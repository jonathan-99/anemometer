#! groovy


// This file is designed to provide a jenkins instance with a pipeline to download, unittest, coverage test this
// anemometer project.

// note jenkins / pipeline doesn't like running python through groovy, so they're extracted to

pipeline {
    agent any
    stages {
        stage('setup 1') {
            steps {
                script {
                    echo "check git, groovy and pip version"
                    sh """
                        chmod +x /jenkins_scripts/setup_checks.sh
                        ./jenkins_scripts/setup_checks.sh
                    """
                }
            }
        }
        stage('download') {
            steps {
                script {
                    echo "git download"
                    sh """
                        rm -rf anemometer
                        git clone https://github.com/jonathan-99/anemometer.git
                    """
                }
            }
        }
        stage('unittest') {
            steps {
                script {
                    try {
                        echo "doing unittests"
                        sh """
                            chmod +x /jenkins_scripts/do_unittests.sh
                            ./jenkins_scripts/do_unittests.sh
                        """
                    } catch(err) {
                        echo "There was an error in unittests $err"
                    }
                }
            }
        }
        stage('coverage') {
            steps {
                script {
                    try {
                        echo "coverage report"
                        sh """
                            chmod +x /jenkins_scripts/do_unittests.sh
                            ./jenkins_scripts/do_unittests.sh
                        """
                    } catch(err) {
                        echo "There was an error in coverage report $err"
                    }
                }
            }
        }
    }
}
