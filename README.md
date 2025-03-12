# airflow-local

## Getting Started

This section describes how to make things do the thing.

### Enabling Kubernetes

Follow the instructions for [enabling Kubernetes in Docker
Desktop][docker-desktop-k8s].

Validate that you can connect to the Kubernetes cluster with `kubectl` and view
the running pods.

[docker-desktop-k8s]: https://docs.docker.com/desktop/kubernetes/

### Quickstart

Make sure Kubernetes is enabled in Docker Desktop.

Run the scripts in the repository in order:

1. `script/bootstrap` - Installs/upgrades required dependencies
2. `script/setup` - Installs ArgoCD and Apps to the docker-desktop cluster
3. `script/server` - Starts port-forwarding and opens a browser to ArgoCD

### Installing ArgoCD

This is how you add ArgoCD to your cluster.

> [!TIP] Setting port-forward options for the ArgoCD CLI
> ArgoCD lets you set CLI options in an environment variable so you don't have
> to retype them every time.
>
> ```bash
> export ARGOCD_OPTS='--port-forward-namespace argocd --port-forward --insecure'
> ```
>
> This lets you run a command like: `argocd account update-password` and it will
> provide the full options like:
> `argocd --port-forward-namespace argocd --port-forward --insecure account update-password`.

#### Restoring from an existing repository

> [!NOTE]
> Prefer using the scripts in the repository.

Use `argocd-autopilot` to restore from this repository. The
[documentation][argocd-autopilot-recover] can be found here.

This will install ArgoCD and Apps to the docker-desktop cluster. It can be run
multiple times if you need to, as the resources will not be recreated.

[argocd-autopilot-recover]: https://argocd-autopilot.readthedocs.io/en/stable/Recovery/#apply-argo-cd-manifests-from-existing-repository

```bash
# Export the repository for easy reference
export GIT_REPO="https://github.com/shakefu/airflow-local"
# Export the token for autopilot to pick up. This uses the GitHub CLI.
export GIT_TOKEN="$(gh auth token)"
# Bootstrap ArgoCD and the Apps
argocd-autopilot repo bootstrap --recover --app "${GIT_REPO}/bootstrap/argo-cd"
```

#### Creating GitHub repository credentials

ArgoCD needs to be able to access our private GitHub repositories, so we create
credentials for that.

```bash
$ argocd repocreds add --upsert https://github.com/shakefu --username git --password "$(gh auth token)"
Repository credentials for 'https://github.com/shakefu' added
$ argocd repo add --upsert https://github.com/shakefu/airflow-local
Repository 'https://github.com/shakefu/airflow-local' added
```

#### Installing via manifests

Ensure you're using your `docker-desktop` Kubernetes context. This can be done
via the Docker Desktop menubar icon, or by manually setting your context using
`kubectl`.

Follow the instructions for [installing ArgoCD][install-argocd] and the [Getting
Started Guide][getting-started-argocd] up to the point where you can open the UI
in a browser and log in with the Admin credentials.

Using the port-fowarding option for accessing the local ArgoCD instance is the
easiest option.

[install-argocd]: https://argo-cd.readthedocs.io/en/stable/getting_started/#1-install-argo-cd
[getting-started-argocd]: https://argo-cd.readthedocs.io/en/stable/getting_started/

#### Installing in HA for Production usage

ArgoCD [provides separate manifests][install-argocd-ha] that provide a highly
available setup for the ArgoCD services and resources. This is what should be
used in Production ArgoCD deployments (e.g. EKS). Locally, in a Docker Desktop
environment, this would waste resources.

[install-argocd-ha]: https://argocd-autopilot.readthedocs.io/en/stable/Advanced-Installation/#high-availability

#### Alternative install via `argocd-autopilot`

This is mostly useful if you're bootstrapping a new ArgoCD repository.

Follow the instructions for [Getting Started with ArgoCD
Autopilot][getting-started-autopilot].

More information can be found in this blog post about [how to use ArgoCD Autopilot][autopilot-in-depth].

[getting-started-autopilot]: https://argocd-autopilot.readthedocs.io/en/stable/Getting-Started/
[autopilot-in-depth]: https://codefresh.io/blog/launching-argo-cd-autopilot-opinionated-way-manage-applications-across-environments-using-gitops-scale/

### Creating a Project

ArgoCD autopilot wants you to create Projects so they can be deployed to
different environments. This may include entirely separate clusters. What's
important to note is that the Project itself doesn't require it strictly. A
single project can be deployed to multiple clusters, or namespaces, as long as
it doesn't require significant material changes to the overlays for each
different environment.

> [!NOTE] Project layout is TBD
> We're still deciding what kind of Project layout we want to have.
