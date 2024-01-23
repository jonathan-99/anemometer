#! groovy


// This file is designed to provide a jenkins instance with a pipeline to download, unittest, coverage test this
// anemometer project.

// def call(body) {
    pipeline {
        agent any
        stages {
            stage('setup 1') {
            steps {
                script {

                    echo "check git version"
                    sh """
                        git --version
                    """
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
            stage('setup 2') {
                steps {
                    script {
                        echo "Installing coverage"
                        withEnv(['PATH+PYTHON=/usr/bin/python3']) {
                            sh """
                                pip install coverage
                            """
                        }
                    }
                }
            }
            stage('unittest') {
                steps {
                    script {
                        try {
                            echo "doing unittests"
                            // change to 'test_*' for full output
                            sh """
                                python3 -m unittest discover -s 'testing/' -v -p 'test_all.py'
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
                                coverage run -m unittest discover -s 'testing/' -v -p 'test_all.py'
                                coverage html -d coverage_report
                            """
                        } catch(err) {
                            echo "There was an error in coverage report $err"
                        }
                    }
                }
            }
        }
    }
// }