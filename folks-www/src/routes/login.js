import axios from "axios";
import { login, flashRedirect, _login } from "../_serverApi.js";

export async function post(req, res) {
  const credentials = req.body;
  const json = await login(credentials).catch(e => {
      if (e.response && e.response.status === 401) {
          return { errors: [e.response.data]}
      }
    return { errors: [e] };
  });
  const isOk = Boolean(json && json.data && json.data.token);

  if (json.data && json.data.token) {
    await _login(json.data, req);
  }

  if (req.headers["x-client-api"]) {
    return res.json(
      isOk
        ? { token: json.data.token, user: { username: json.data.username } }
        : { errors: json.errors || [{ message: "Wrong credentials" }] }
    );
  }

  flashRedirect(req, res, {
    msg: isOk ? "Залогинились" : "Не получилось",
    to: isOk ? "/feed" : "/login"
  });
}
