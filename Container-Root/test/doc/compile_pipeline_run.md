# How-to: Compile a pipeline locally and run remotely through a POST request

## Setting up the environment

This section assumes the need for a secure forwarding of the main romario service port `30966` to `localhost:30966`. In most cases the pipeline creation work can occur outside the cluster context, which in turn requires a secure way of submitting the request.

Romario service binds the service upload port to `30966` at the cluster node level. It is expected that a cluster managing node can forward a connection to a `CLUSTER_NODE0_NAME:30966` port. Hence we can create a secure ssh connection from the pipeline working environment - a.k.a __localhost__ - to a managing node of the cluster and listen at `localhost:30966`. The ssh connection can be done through:

```sh
ssh -i ${PRIVATE_KEY_PATH} username@${MGMT_NODE_IP} -L 30966:${CLUSTER_NODE0_NAME}:30699
```

In this context, the managing node under the `MGMT_NODE_IP` is the node used to configure `kubectl` and contains all cluster, user and context info.

If working on the managing node, the endpoint of the romario's pod is accessible directly and the `post_k8s_run_test.sh` script takes care of finding where to POST the file. An URL pointing to this endpoint can be provided, however is not recommended to be exposed to the public internet.

### Compiling and posting in a single line:

From your local working clone of the [romario repo](http://github.com/bhgedigital/romario), start a romario container with `run.sh`

Compile the pipeline within the container:

```sh
./exec.sh python /wd/Container-Root/pipelines/recursive_while.py
```
curl from __localhost__ into mapped port:

```sh
./Container-root/test/local_post_k8s_run_test.sh Container-Root/pipelines/recursive_while.py.tar.gz
```

## Writing a compilable pipeline

The simplest way of writing a compilable pipeline is to provide a python script with the pipeline object definitions and add an `if __name__ == '__main__':` section to the end of the file, with the direct call for the compiler:

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
