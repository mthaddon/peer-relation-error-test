# peer-relation-error-test

To reproduce the error we would do the following, but it doesn't seem to be
actually causing an error. Looks like the peer relation hooks are firing even
though the unit goes into error state as a result of the nginx-route relation
error.

```
charmcraft pack
juju add-model peer-test
juju deploy nginx-ingress-integrator
juju trust nginx-ingress-integrator --scope=cluster
# Make sure to do the next two in quick sequence
juju deploy ./peer-relation-error-test_ubuntu-22.04-amd64.charm
juju relate nginx-ingress-integrator peer-relation-error-test
# Charm should go into error state. Confirm the peer-ok-relation hooks haven't
# fired. Output of the next command should be empty
juju debug-log --no-tail --replay | grep peer-ok
# Now update config. Nothing should happen because we're in error state.
juju config peer-relation-error-test relation-ok=true
# Now kill the pod
kubectl delete pod peer-relation-error-test-0
# Now see if our peer relation has fired. It shouldn't have
juju debug-log --no-tail --replay | grep peer-ok
```
