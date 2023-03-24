#!/bin/bash
quasar build
cp dist/spa/index.html ../back/index/templates/index/
rm ../back/assets/*;
cp -R dist/spa/assets ../back/
cp dist/spa/favicon.ico ../back/index/static/index/

