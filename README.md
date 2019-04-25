# Romario

_"You give it the ball... it will score!" - Romario, a RESTful API for kick-starting [Kubeflow Pipelines](https://github.com/kubeflow/pipelines) in your Kubernetes cluster._

The intent of _romario_ is to enable large scale runs of _KF Pipelines_, across multiple Kubernetes clusters. _KF Pipelines_ are a key way to "pythonically" orchestrate analytics pipelines, due to its straightforward abstraction of [ARGO](https://github.com/argoproj) into a Python based DSL.

For the background on the scale required for Industrial applications of ML and AI please check [this](https://www.youtube.com/watch?v=rJNSdUjjkic) and [this](https://www.youtube.com/watch?v=dIZt-Ahzew0) talk from Google Cloud NEXT 2019.

## Documentation

[Romario](https://github.com/bhgedigital/romario) provides a REST API, for executing the most usual operations performed by [KF Pipelines](https://github.com/kubeflow/pipelines).

### Building the _Romario_ Project

As any [Depend-on-Docker](https://github.com/bhgedigital/depend-on-docker) project, building _Romario_ is quite easy. Once the `.env` environment file is set, it is enough to execute `build.sh`. Please refer to the [Depend-on-Docker Documentation](https://github.com/bhgedigital/depend-on-docker/blob/master/README.md) for more information on how to customize _Romario_.

### Deployment to a Kubernetes cluster

The deployment of [romario](https://github.com/bhgedigital/romario) assumes the existence of a Kubernetes cluster, with Kubeflow already deployed. The user must have access to the management node of such cluster, so that the deployment happens in the correct namespace (usualy 'kubeflow'). Please refer to [this documentation]() on how to provision such infrastructure.

Once in the management node, _romario_ gets deployed by simply running the `deploy_romario_from_master.sh` script provided [here](https://github.com/bhgedigital/romario/blob/master/Container-Root/k8s/deploy_romario_from_master.sh).

All configurations required for the _romario_ Kubernetes Service and Deployment are given [here](https://github.com/bhgedigital/romario/blob/master/Container-Root/k8s/service_deployment_romario.yaml). Other nifty automation of usual `kubectl` commands are provided in the same [k8s](https://github.com/bhgedigital/romario/tree/master/Container-Root/k8s) folder.


### Running a Pipelines

Executing a simple pipeline is easy from the Master node of the underlying Kubernetes cluster. A sample `curl -x POST ...` example is available in [romario/Container-Root/test](https://github.com/bhgedigital/romario/blob/master/Container-Root/test/post_k8s_run_test.sh). The script takes a single argument of the `.tar.gz` tarball. From the _romario_ root:

``` bash
./Container-Root/test/post_k8s_run_test.sh Container-Root/pipelines/SampleBasic-Condition.yaml.tar.gz
```

A [Swagger-UI](https://swagger.io/tools/swagger-ui/) is available at https://\<romario-endpoint\>/apidocs .   

### Running _romario_ image as a Jupyter Notebook server

Running a Jupyter Notebook server from the Master node on the cluster is simple with _romario_ and _Depend-on-Docker_. Simply execute:

```bash
./run_jupyter.sh
```

This script will map the whole _romario_ root to `/wd`, allowing for the user to compile Pipelines manually from the master. A `POST` request method to compile pipelines described in `.py` scripts is under construction, stay tuned!  

### Known Features, a.k.a Bugs

1. Pipelines should be POST as `tar.gz` files, currently POSTing `yaml` will result in an exception.

## Disclosures & Acknowledgments

[Romario](www.github.com/bhgedigital) wraps the Python DSL from [Kubeflow Pipelines](https://github.com/kubeflow/pipelines), providing minimal functionality through key endpoints - mostly _kfp.client.run_pipeline()_ method. The opensource version of Romario is __NOT__ intended to be an exhaustive production ready service.  

The Pipelines team has been very supportive and we are very grateful.
