const mongoose = require("mongoose");
const connect = mongoose.connect("mongodb+srv://Yuvi04:login123@login-tut.ryx9acd.mongodb.net/?retryWrites=true&w=majority&appName=Login-Tut");


connect.then(()=>{
    console.log("Connected to the database");
})
.catch(()=>{
    console.log("Error while connecting to the database");
});

const LoginSchema = new mongoose.Schema({
    name: {
        type: String,
        required: true
    },
    password: {
        type: String,
        required: true
    }
});

const collection = mongoose.model("users", LoginSchema);

module.exports = collection;