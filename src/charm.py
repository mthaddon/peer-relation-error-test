#!/usr/bin/env python3
# Copyright 2024 Tom Haddon
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""Charm the service.

Refer to the following tutorial that will help you
develop a new k8s charm using the Operator Framework:

https://juju.is/docs/sdk/create-a-minimal-kubernetes-charm
"""

import logging
import time

import ops

# Log messages can be retrieved using juju debug-log
logger = logging.getLogger(__name__)

VALID_LOG_LEVELS = ["info", "debug", "warning", "error", "critical"]


class PeerRelationErrorTestCharm(ops.CharmBase):
    """Charm the service."""

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.config_changed, self._on_config_changed)
        self.framework.observe(self.on.do_it_action, self._on_do_it_action)
        self.framework.observe(self.on.nginx_route_relation_created, self._on_nginx_route_relation_created)
        self.framework.observe(self.on.peer_ok_relation_created, self._on_peer_ok_relation_created)

    def _on_do_it_action(self, event):
        event.set_results({"result": "I did it!"})

    def _on_nginx_route_relation_created(self, _):
        if not self.model.config["relations-ok"]:
            raise Exception("Our nginx-route-relation has been created but we're not okay")

    def _on_peer_ok_relation_created(self, _):
        time.sleep(10)
        logger.info("Peer OK relation created")

    def _on_config_changed(self, event: ops.ConfigChangedEvent):
        """Handle changed configuration."""
        # Fetch the new config value
        log_level = self.model.config["log-level"].lower()
        logger.info("relations-ok is set to %s", self.model.config["relations-ok"])

        # Do some validation of the configuration option
        if log_level in VALID_LOG_LEVELS:
            logger.debug("Log level changed to '%s' (but we don't have a workload)", log_level)
            self.unit.status = ops.ActiveStatus()
        else:
            # In this case, the config option is bad, so block the charm and notify the operator.
            self.unit.status = ops.BlockedStatus("invalid log level: '{log_level}'")


if __name__ == "__main__":  # pragma: nocover
    ops.main(PeerRelationErrorTestCharm)  # type: ignore
