# Adventure-Ballad

### Youtube Link: https://www.youtube.com/watch?v=7Hi9ufictg4


## Getting Started

### Start Backend

### Obtain the cookie of your app.suno.ai account

1. Head over to [app.suno.ai](https://app.suno.ai) using your browser.
2. Open up the browser console: hit `F12` or access the `Developer Tools`.
3. Navigate to the `Network tab`.
4. Give the page a quick refresh.
5. Identify the request that includes the keyword `client?_clerk_js_version`.
6. Click on it and switch over to the `Header` tab.
7. Locate the `Cookie` section, hover your mouse over it, and copy the value of the Cookie.

![get cookie](https://github.com/gcui-art/suno-api/blob/main/public/get-cookie-demo.gif)

### Install NPM depenencies

```bash
cd Backend/suno-api
npm install
```
be sure to add the following to your `.env` file:

```bash
SUNO_COOKIE=<your-cookie>
```

### Run suno api

    Run `npm run dev`.


### Switch to Python Backend


```bash
cd ../
```

### Activate Environment

```bash
python3 -m venv myenv
source myenv/bin/activate
```

### Install requirements

```
pip3 install -r requirements.txt
```

### Set Gemini API

```bash
 set -x API_KEY "Your_Api_Key"  
```
### Run Server

```bash
python3 new_server.py
```

### Move to Frontend and start it.

```bash
cd ../Frontend/adventure_ballad
flutter run
```

