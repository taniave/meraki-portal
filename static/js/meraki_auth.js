var CognitoUserPool = AmazonCognitoIdentity.CognitoUserPool;
var CognitoUser = AmazonCognitoIdentity.CognitoUser;
var AuthenticationDetails = AmazonCognitoIdentity.AuthenticationDetails;

var poolData = {
    UserPoolId: 'USER-POOL-ID', // Your user pool id here
    ClientId: 'CLIENT-ID', // Your client id here
};


// Parse paramaters
var base_grant_url = decodeURIComponent(GetURLParameter("base_grant_url"));
var user_continue_url = decodeURIComponent(GetURLParameter("user_continue_url"));
var node_mac = GetURLParameter("node_mac");
var client_ip = GetURLParameter("client_ip");
var client_mac = GetURLParameter("client_mac");

// Print Meraki provided paramaters for Debugging State
/*console.log("user_continue_url: "+user_continue_url);
console.log("client_ip: "+client_ip);
document.getElementById("baseGrantURL").innerHTML = base_grant_url;
document.getElementById("userContinueURL").innerHTML = user_continue_url;
document.getElementById("clientIP").innerHTML = client_ip;
document.getElementById("clientMAC").innerHTML = client_mac;
document.getElementById("nodeMAC").innerHTML = node_mac;*/

// Form Submit handler.
/*document.getElementById('account').onsubmit= function(e){
    e.preventDefault(); //prevents default form submission process to allow login and validation
    //login();
} */
document.getElementById('loginForm').onsubmit= function(e){
    e.preventDefault(); //prevents default form submission process to allow login and validation
    //login();
}

// ******************
// Login to Meraki by redirecting client to the base_grant_url 
// 
// The logingUrl will add a continue_url parameter for a final client
// redirect to their intended site. 
// (you could override this url to send the user to a home page)
// ****************** 
function authUser(){

    var loginUrl = base_grant_url;
    if(user_continue_url !== "undefined"){
        loginUrl += "?continue_url="+user_continue_url;
    }
    console.log("Logging in... ",loginUrl);
    // redirect browser to meraki auth URL.
    window.location.href = loginUrl;
}

// Button handler function to store the form data and login. 
/*function login(){
    // send the data somewhere like a database
    var data = {};
    data.name = document.getElementById("name").value;
    data.name_ap = document.getElementById("name_ap").value;
    data.name_am = document.getElementById("name_am").value;
    data.email = document.getElementById("email").value;
    alert("Hello "+data.name + data.name_ap + data.name_am +"\n"+"Thanks for providing your email: "+data.email);
    console.log("Storing data to db...", data);
    

    // Complete Login
    authUser();
    signIn();
}*/

// Helper function to parse URL
function GetURLParameter(sParam)
{
    var sPageURL = window.location.search.substring(1);
    var sURLVariables = sPageURL.split('&');
    for (var i = 0; i < sURLVariables.length; i++) 
    {
        var sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0] == sParam) 
        {
            return sParameterName[1];
        }
    }
}

function signIn () {
    var username = $('#email').val();
    var password = $('#password').val();

    console.log(username);
    console.log(password);
    var authenticationData = {
        Username: username,
        Password: password,
    };
    var authenticationDetails = new AuthenticationDetails(authenticationData);

    var userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);
    var userData = {
        Username: username,
        Pool: userPool,
    };
    var cognitoUser = new CognitoUser(userData);
    cognitoUser.authenticateUser(authenticationDetails, {
        onSuccess: function(result) {
            var accessToken = result.getAccessToken().getJwtToken();
            console.log('access token + ' + accessToken );
            //authUser();
            //document.getElementById("loginForm").submit();
            window.location.href='/log';
    
          /*  //POTENTIAL: Region needs to be set if not already set previously elsewhere.
            AWS.config.region = '<region>';
    
            AWS.config.credentials = new AWS.CognitoIdentityCredentials({
                IdentityPoolId: '...', // your identity pool id here
                Logins: {
                    // Change the key below according to the specific region your user pool is in.
                    'cognito-idp.<region>.amazonaws.com/<YOUR_USER_POOL_ID>': result
                        .getIdToken()
                        .getJwtToken(),
                },
            });
    
            //refreshes credentials using AWS.CognitoIdentity.getCredentialsForIdentity()
            AWS.config.credentials.refresh(error => {
                if (error) {
                    console.error(error);
                } else {
                    // Instantiate aws sdk service objects now that the credentials have been updated.
                    // example: var s3 = new AWS.S3();
                    console.log('Successfully logged!');
                }
            });*/
        },
    
        onFailure: function(err) {
            alert(err.message || JSON.stringify(err));
        }
    });

}

function register () {
    var name = $('#name').val();
    var name_mid = $('#name_mid').val();
    var name_ap = $('#name_ap').val();
    var name_am = $('#name_am').val();
    var username = $('#email').val();
    var password = $('#password').val();
    var email = $('#email').val();

    console.log(name);
    console.log(name_mid);
    console.log(name_ap);
    console.log(name_am);
    console.log(username);
    console.log(password);
    console.log(email);
    
    var userPool = new CognitoUserPool(poolData);
    
    var attributeList = [];
    
    var dataEmail = {
        Name: 'email',
        Value: email,
    };
    
    
    var attributeEmail = new AmazonCognitoIdentity.CognitoUserAttribute(dataEmail);
    /*var attributePhoneNumber = new AmazonCognitoIdentity.CognitoUserAttribute(
        dataPhoneNumber
    );*/
    
    attributeList.push(attributeEmail);
    //attributeList.push(attributePhoneNumber);
    
    

    userPool.signUp(username, password, attributeList, null, function(err, result) {
        if (err) {
            alert(err.message || JSON.stringify(err));
            return;
        }
        cognitoUser = result.user;
        console.log('user name is ' + cognitoUser.getUsername());
        window.location.href='/code';
    });
}

function confirmCode () {
    var username = $('#code_username').val();
    var code = $('#code_code').val();

    var userPool = new CognitoUserPool(poolData);
    var userData = {
        Username: username,
        Pool: userPool,
    };
    
    var cognitoUser = new CognitoUser(userData);
    cognitoUser.confirmRegistration(code, true, function(err, result) {
        if (err) {
            alert(err.message || JSON.stringify(err));
            return;
        }
        console.log('call result: ' + result);
        window.location.href = "/index";
    });

    //window.location.href = "/index";
}

function signOut () {
    
    var userPool = new CognitoUserPool(poolData);
    var cognitoUser = userPool.getCurrentUser();
    //console.log('sign out');
    if(cognitoUser !== null){
        cognitoUser.signOut();
    }

    window.location.href = "/index";
}

function setWelcome(){

    var userPool = new CognitoUserPool(poolData);
    var cognitoUser = userPool.getCurrentUser();
    
    if (cognitoUser != null) {
        cognitoUser.getSession(function(err, session) {
            if (err) {
                alert(err.message || JSON.stringify(err));
                return;
            }
            //console.log('session validity: ' + session.isValid());
            console.log(cognitoUser.signInUserSession.accessToken.jwtToken);
            $('#username').html(cognitoUser.username);
           /* // NOTE: getSession must be called to authenticate user before calling getUserAttributes
            cognitoUser.getUserAttributes(function(err, attributes) {
                if (err) {
                    // Handle error
                } else {
                    // Do something with attributes
                }
            });
    
            AWS.config.credentials = new AWS.CognitoIdentityCredentials({
                IdentityPoolId: '...', // your identity pool id here
                Logins: {
                    // Change the key below according to the specific region your user pool is in.
                    'cognito-idp.<region>.amazonaws.com/<YOUR_USER_POOL_ID>': session
                        .getIdToken()
                        .getJwtToken(),
                },
            });*/
    
            // Instantiate aws sdk service objects now that the credentials have been updated.
            // example: var s3 = new AWS.S3();
        });
    }


}




function onSignIn(googleUser) {
    var profile = googleUser.getBasicProfile();
    console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
    console.log('Name: ' + profile.getName());
    console.log('Image URL: ' + profile.getImageUrl());
    console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.
  }

  
  function signinCallback(authResult) {
    if (authResult['status']['signed_in']) {
  
       // Add the Google access token to the Amazon Cognito credentials login map.
       AWS.config.credentials = new AWS.CognitoIdentityCredentials({
          IdentityPoolId: 'us-east-2_bDahZBIQc',
          Logins: {
             'accounts.google.com': authResult['id_token']
          }
       });
  
       // Obtain AWS credentials
       AWS.config.credentials.get(function(){
          // Access AWS resources here.
       });
    }
  }


function onLibraryLoaded() {
    gapi.load('auth2', function() {
        gapi.auth2.init({
            client_id: '206071216297-jrsp297bt4hs5kppd7mm38q6g7fp5eg5.apps.googleusercontent.com',
            scope: 'profile'
        })
    });
}

function onSignInClicked() {
    gapi.load('auth2', function() {
        gapi.auth2.signIn().then(function(googleUser) {
          console.log('user signed in');
          window.location.href = "/log";
        }, function(error) {
            console.log('user failed to sign in');
        })
    });
}



function cita(){
    document.getElementById("loginForm").submit();
    //window.location.href = "/cita";
}