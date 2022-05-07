#!/bin/bash
comando='sudo microk8s kubectl'

$comando apply -f joaquin.yaml

$comando apply -f joaquin_service.yaml

