# We Race Here

## Deploy:
1. On local dev run build_release.sh. This will build the frontend, tag the release and push to master.
2. On server, dev or prod, run `wrh_organization_deploy` (not deploy.sh) This will pull the latest build.

## Installing:

### Backend Prod
- Currently, prodction is running on Ubuntu 22.04 (LTS)
- There is a install script in the utils folder.
- runs under user appuser

### Backend Dev
- For developement, use python 3.10+
- run pip install -r requirement.txt

### Frontend
1. Install all packages

   ```bash
   yarn

   # npm install [for npm]
   
   # to reset
   # be sure you are using node version 16 or lower
   # remove previous node_modules folder
   npm install --force
   npm install vue@2.6.14 vue-template-compiler@2.6.14 --force
   npm run serve
   ```

2. Run development server

   ```bash
   yarn serve

   # npm run serve [for npm]
   ```

3. Generate build files for deployment

   ```bash
   yarn build

   # npm run build [for npm]
   ```

#### Documentation

Please read the [documentation](https://themeselection.com/demo/materio-vuetify-vuejs-admin-template/documentation) for getting started.

#### Support

Visit [Getting Support](https://themeselection.com/demo/materio-vuetify-vuejs-admin-template/documentation/guide/getting-started/support.html) guide for getting support for materio admin.

#### Updating the template

Visit article on [updating the template](https://themeselection.com/demo/materio-vuetify-vuejs-admin-template/documentation/articles/how-to-update-materio-to-latest-version.html) to latest version.

## License Details

For details about license please check the [`LICENSE.md`](https://github.com/themeselection/materio-vuetify-vuejs-admin-template/blob/main/LICENSE.MD) file in the root of the GitHub repository. You can also read more about licensing here: [https://store.vuetifyjs.com/licenses](https://store.vuetifyjs.com/licenses)


