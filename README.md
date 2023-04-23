# Datalake repo

In this repo, I keep multiple Python packages that are used for defining datalake resources as Infrastructure as Code on AWS.

These packages can be used independently, and might be published to Pypi in the future.

## datalake-lib

This package contains some interfaces and classes that model the Glue concepts. This package contains the highest level of abstraction, and can be used independently of the other packages which are IaC tooling specific.

## datalake-cdk

This package contains constructs to deploy Glue entities as resources to AWS making use of CDK. The `app.py` file contains the actual instantiation and definition of the CDK stack containing the resources.

This package uses the datalake-lib package.
