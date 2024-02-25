#! groovy


// This file is designed to provide a jenkins instance with a pipeline to download, unittest, coverage test this
// anemometer project.

// note jenkins / pipeline doesn't like running python through groovy, so they're extracted to

pipeline {
    agent any
    stages {
        stage('checks') {
            steps {
                script {
                    sh """
                        echo "this is the npm version ${sh(script: 'git --version', returnStdout: true).trim()}"
                        echo "this is the npm version ${sh(script: 'python --version', returnStdout: true).trim()}"
                        echo "this is the npm version ${sh(script: 'sudo ufw status', returnStdout: true).trim()}"
                        echo "this is the npm version ${sh(script: 'docker -v', returnStdout: true).trim()}"
                    """
                }
            }
        }
        stage('setup 1') {
            steps {
                script {
                    sh """
                        file='jenkins_scripts/setup_checks.sh'
                        chmod +x \$file
                        filePermissions=\$(ls -l \$file)
                        echo "File permissions: \$filePermissions"
                        script -q -c "./\$file" /dev/null
                    """
                }
            }
        }
        stage('download and install docker image') {
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
