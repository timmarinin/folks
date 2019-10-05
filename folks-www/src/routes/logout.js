import axios from "axios";
import { logout, flashRedirect } from "../_serverApi.js";

export async function get(req, res) {
  logout(req);
  setTimeout(() => {
    res.statusCode = 302
    res.setHeader('Location', '/')
    res.end()
  }, 50)
}
