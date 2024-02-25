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
        stage('download and install docker image with dependencies') {
            steps {
                script {
                    sh """
                        file1='jenkins_scripts/download_and_install.sh'
                        chmod +x \$file1
                        filePermissions=\$(ls -l \$file1)
                        echo "File permissions: \$filePermissions"
                        script -q -c ".\$file1" /dev/null
                    """
                }
            }
        }
        stage('unittest, PEP8, coverage report') {
            steps {
                script {
                    sh """
                        file2='jenkins_scripts/do_unittests.sh'
                        chmod +x \$file2
                        filePermissions=\$(ls -l \$file2)
                        echo "File permissions: \$filePermissions"
                        script -q -c ".\$file2" /dev/null
                    """
                }
            }
        }
    }
}
