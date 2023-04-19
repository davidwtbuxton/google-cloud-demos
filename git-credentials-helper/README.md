Git credentials helper
======================

Git credentials helper for use with Google Cloud Build.

This is useful when your build step accesses resources on a password-protected git host such as some *.googlesource.com repositories, but where the step's image does not include the gcloud SDK (for example when using the official node images). The credentials helper gets an auth token for the Cloud Build service account, usually `[PROJECT_NUMBER]@cloudbuild.gserviceaccount.com`.

Add the `githelper.py` script to your source code repository. Then use this in
a script step in the Cloud Build job. Node images include Python 3, so you
can use this helper like:

    # cloudbuild.yaml
    steps:
      - name: node:16
        script: |
          set -o errexit -o nounset
          # And `set -o pipefail` when using bash.
          _helper="/workspace/githelper.py"
          chmod a+x "$_helper"
          git config --system credential.helper "$_helper"
          npm ci

Related documentation:

- [Custom helpers][1] for git credentials.
- [Authenticating applications directly with access tokens][2] on Compute Engine instances.
- [Running bash scripts][3] in Cloud Build steps.
- [Tools for Google Compute Engine][4].
- [Cloud Build service account][5].

[1]: https://git-scm.com/docs/gitcredentials#_custom_helpers
[2]: https://cloud.google.com/compute/docs/access/create-enable-service-accounts-for-instances#applications
[3]: https://cloud.google.com/build/docs/configuring-builds/run-bash-scripts
[4]: https://gerrit.googlesource.com/gcompute-tools/
[5]: https://cloud.google.com/build/docs/cloud-build-service-account
