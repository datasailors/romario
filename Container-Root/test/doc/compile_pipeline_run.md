# How-to: Compile a pipeline locally and run remotely through a POST request


## Compiling and posting in a single line:

Start container with `run.sh`

Execute compilation within the container and curl from localhost into mapped port:

```bash
./exec.sh python /wd/Container-Root/pipelines/recursive_while.py && ./Container-root/test/local_post_k8s_run_test.sh Container-Root/pipelines/recursive_while.py.tar.gz
```
