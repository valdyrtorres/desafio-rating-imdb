pipeline {
    agent any
    
    environment {
        DOCKER_COMPOSE_FILE = 'docker-compose.yml'
        APP_NAME = 'movie-review-api'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup Environment') {
            steps {
                script {
                    // Create .env file from Jenkins credentials
                    withCredentials([
                        string(credentialsId: 'OMDB_API_KEY', variable: 'OMDB_API_KEY')
                    ]) {
                        writeFile file: '.env', text: """
DATABASE_URL=postgresql+asyncpg://user:password@db:5432/moviedb
OMDB_API_KEY=${OMDB_API_KEY}
DEBUG=False
HOST=0.0.0.0
PORT=8000
"""
                    }
                }
            }
        }
        
        stage('Build') {
            steps {
                script {
                    sh 'docker-compose build'
                }
            }
        }
        
        stage('Test') {
            steps {
                script {
                    sh 'docker-compose run --rm app python -m pytest tests/ -v'
                }
            }
        }
        
        stage('Deploy') {
            steps {
                script {
                    sh 'docker-compose down || true'
                    sh 'docker-compose up -d'
                    
                    // Wait for services to be ready
                    sh 'sleep 30'
                    
                    // Health check
                    sh 'curl -f http://localhost:90/health || exit 1'
                }
            }
        }
    }
    
    post {
        always {
            // Cleanup
            sh 'docker-compose logs'
        }
        
        failure {
            // Rollback on failure
            sh 'docker-compose down || true'
        }
        
        success {
            echo 'Deployment successful!'
        }
    }
}