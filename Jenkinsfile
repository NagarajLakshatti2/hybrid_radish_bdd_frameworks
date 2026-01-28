pipeline {
    agent any

    environment {
        GH_PAGES_BRANCH = "gh-pages"
    }

    stages {

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t radish-bdd .'
            }
        }

        stage('Run Tests & Generate Report') {
            steps {
                sh '''
                docker run --rm \
                  -v $WORKSPACE/reports:/app/reports \
                  radish-bdd
                '''
            }
        }

        stage('Publish to GitHub Pages') {
            steps {
                sh '''
                rm -rf gh-pages
                git clone -b gh-pages https://github.com/${GIT_URL#*github.com/} gh-pages || git clone https://github.com/${GIT_URL#*github.com/} gh-pages
                cd gh-pages
                git checkout -B gh-pages
                rm -rf *
                cp -r ../reports/html/* .
                git add .
                git commit -m "📊 Update BDD report - $(date)" || echo "No changes"
                git push origin gh-pages
                '''
            }
        }
    }
}
