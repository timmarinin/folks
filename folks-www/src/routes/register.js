import axios from "axios";
import { register, flashRedirect, _login } from "../_serverApi.js";

export async function post(req, res) {
  const credentials = req.body;
  const json = await register(credentials).catch(e => {
    if (e.response) {
      return { errors: [e.response.data] };
    }
    return { errors: [e] };
  });
  const isOk = Boolean(json && json.data && json.data.token);
  if (isOk) {
    _login(json.data, req);
  }
  if (req.headers["x-client-api"]) {
    return res.json(
      isOk
        ? { token: json.data.token, user: json.data.user }
        : { errors: json.errors || [{ message: "Wrong credentials" }] }
    );
  }

  flashRedirect(req, res, {
    msg: isOk ? "Зарегистрировались" : "Не получилось",
    to: isOk ? "/feed" : "/register"
  });
}
