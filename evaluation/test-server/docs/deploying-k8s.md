# Deploying k8s

## Running k8s on Amazon EC2

Based on this [guide](http://kubernetes.io/docs/getting-started-guides/aws/).

#### Prerequisites

Before beginning we need:
- An AWS Account
- An installed, configured AWS CLI
  - `pip install awscli`
  - Create the user `mattjmcnaughton` with IAM, and pass along the ID and key
    when asked with `aws configure`.
  - For said user, attach the `AmazonEC2FullAccess`, `AmazonS3FullAccess`
    and the `IAMFullAccess` policies.
- An AWS instance profile and role with full access to EC2.
  - `aws iam create-instance-profile --instance-profile-name default`
  - In the `IAM` dashboard create a new role, entitled `DefaultRole` and give it
    full permissions to access `AmazonEC2` and `AmazonS3`.
  - `aws iam add-role-to-instance-profile --role-name DefaultRole
    --instance-profile-name default`

#### Starting k8s

- *k8s will build a version from the current k8s code, so be sure to check out
  the branch/version I want*
- To turnup a cluster:
  - First, build an instance of k8s
    - `make clean`
    - `make quick-release`
      - If necessary, increase the memory of the virtual machine hosting the
        docker daemon.
      - Additionally, if necessary pause Dropbox syncing.
  - Then, run the instance.
    - `export KUBERNETES_PROVIDER=aws; cluster/kube-up.sh`
  - Kubectl will already be configured to work, so can just run `kubectl`.

## Deploying k8s objects to k8s

- To deploy a replication controller/service/hpa, use `kubectl create -f
  YAML_NAME`
- Deploy a load balancing service - to get the IP for that service, do...
  - `kubectl describe svc SERVICENAME`
    - The `LoadBalancer Ingress` value is where we want to send requests (being
      sure to use the correct port).

## Automating

## Tearing down Kubernetes

- The majority of the AWS services utilized by k8s will be deleted when running
  `cluster/kube-down.sh`.
- Currently it is necessary to manually delete the `S3` bucket, although the
  costs of keeping it hosted are likely very low.
- k8s creates resources in the `us-west-2` region, so be sure to look for
  resources there.
