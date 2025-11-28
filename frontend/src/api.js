import axios from "axios";

const client = axios.create({
  baseURL: "/api/tasks",
  timeout: 10000,
});

export async function analyzeTasks(tasks, strategy) {
  const { data } = await client.post("/analyze/", { tasks, strategy });
  return data;
}

export async function getSuggestions() {
  const { data } = await client.get("/suggest/");
  return data;
}

