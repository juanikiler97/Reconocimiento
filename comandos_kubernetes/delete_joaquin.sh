#!/bin/bash
comando='sudo microk8s kubectl'

#$comando get pods
$comando delete deployment joaquin
$comando delete service joaquin
