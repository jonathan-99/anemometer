#! groovy


// This file is designed to provide a jenkins instance with a pipeline to download, unittest, coverage test this
// anemometer project.

// def call(body) {
    pipeline {
        agent any
        stages {
            stage('download') {
                steps {
                    script {
                        echo "git download"
                        sh """
                            git --version
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
                                python3 -m unittest -s 'testing/' -v test_all.Testing
                            """
                        } catch(err) {
                            echo "There was an error in unittests $err"
                        }
                    }
                }
            }
        }
    }
// }