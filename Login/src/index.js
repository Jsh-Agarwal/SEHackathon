const express = require("express");
const path = require("path");
const bcrypt = require("bcrypt");
const axios = require("axios");
const getCollection = require("./config");

const app = express();

//data to json
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

//ejs as view engine
app.set('view engine', 'ejs');  

//static file
app.use(express.static("public"));

let collection;

getCollection().then(col => {
    collection = col;
}).catch(err => {
    console.error(err);
});

app.get("/", async(req, res) => {
    res.render("login");
});

app.get("/signup", async(req, res) => {
    res.render("signup");
});

//reg user
app.post("/signup", async(req, res) => {

    const data = {
        name: req.body.username,
        password: req.body.password
    }

    //existing user
    const existinguser = await collection.findOne({name: data.name});

    if(existinguser){
        res.send("User already exists");
    }else{
        //hash password
        const saltRounds = 10;
        const hashedPassword = await bcrypt.hash(data.password, saltRounds);
        data.password = hashedPassword;
        //replace hash pass with og pass

        const userdata = await collection.insertOne(data);
        console.log(userdata);

        const documentId = "DOCUMENT_ID_HERE"; // Replace with the actual document ID
        const phoneNumber = "RECIPIENT_PHONE_NUMBER"; // Replace with the recipient's phone number

        axios.post("http://flask_server_host:flask_server_port/send_pdf", {
            document_id: documentId,
            phone_number: phoneNumber
        })
        .then(response => {
            console.log(response.data);
            res.render("home");
        })
        .catch(error => {
            console.error(error);
            res.send("Error sending PDF");
        });
    }
});

//login user
app.post("/login", async(req, res) => {
    try{
        const check = await collection.findOne({name: req.body.username});
        if(!check){
            res.send("User not found");
        }
        //compare password
        const isPasswordMatch = await bcrypt.compare(req.body.password, check.password);
        if(isPasswordMatch){
            res.render("home");
        }else{
            res.send("Wrong Password");
        }   
    } catch{
        res.send("Wrong details!");
    }
})

const port = 5000;
app.listen(port,() => {
    console.log(`Server is running on Port: ${port}`);
})