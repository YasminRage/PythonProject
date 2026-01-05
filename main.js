const port = 3000;
const express = require('express')
const app = express()


app.post("/contact", (req, res) => {
res.send("Contact information submitted successfully.");
});

app.use((req, res, next) => {
console.log(`request made to: ${req.url}`);
next();
});

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
