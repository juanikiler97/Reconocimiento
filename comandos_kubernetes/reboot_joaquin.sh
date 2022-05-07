#!/bin/bash
comando='sudo microk8s kubectl'

$comando delete deployment joaquin
$comando apply -f joaquin.yaml

