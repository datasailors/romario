# How-to: Compile a pipeline locally and run remotely through a POST request

## Setting up the environment

This section assumes the need for secure forwarding of the main romario service port `30966` to `localhost:30966`. In most cases the pipeline creation work can occur outside the cluster context, which in turn requires a secure way of submitting the request.

The Romario service exposes the service upload port on node port `30966`. This means that any node in the cluster exposes the service on this port. It is expected that a management VM can forward a connection to `CLUSTER_NODE0_NAME:30966`. Hence we can create a secure ssh connection from a local pipeline working environment - a.k.a __localhost__ - to the management vm and listen at `localhost:30966`. The ssh tunnel can be created through the following command:

```sh
ssh -i ${PRIVATE_KEY_PATH} username@${MGMT_NODE_IP} -L 30966:${CLUSTER_NODE0_NAME}:30699
```

In this context, the management VM under the `MGMT_NODE_IP` is the VM that is configured to execute `kubectl` commands against the Kubernetes cluster.

If working on the management VM, the endpoint of the Romario's pod is accessible directly and the `post_k8s_run_test.sh` script takes care of finding where to POST the file. An URL pointing to this endpoint can be provided, however is not recommended to be exposed to the Internet.

## Compiling and running pipeline with single lines:

From your local working clone of the [romario repo](http://github.com/bhgedigital/romario), start a romario container with `run.sh`

Compile the pipeline within the container:

```sh
./exec.sh python /wd/Container-Root/pipelines/recursive_while.py
```

curl from __localhost__ into mapped port for execution:

```sh
./Container-root/test/local_post_k8s_run_test.sh Container-Root/pipelines/recursive_while.py.tar.gz
```

## Writing a compilable pipeline

The simplest way of writing a compilable pipeline is to provide a python script with the pipeline object definitions and add an `if __name__ == '__main__':` section to the end of the file, with the direct call for the compiler as shown below:

```python
...
@dsl.pipeline(
    name='my-pipeline',
    description='My first pipeline.'
)
def main_pipeline():
  ...

if __name__ == '__main__':
  import kfp.compiler as compiler
  compiler.Compiler().compile(main_pipeline, __file__ + '.tar.gz')
```

Several examples of compilable pipelines are available in the __compiler__ section of the [python sdk](https://github.com/kubeflow/pipelines/tree/master/sdk/python/tests/compiler/testdata).
