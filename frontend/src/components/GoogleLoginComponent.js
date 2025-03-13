import React from "react";
import { GoogleLogin } from "@react-oauth/google";

const GoogleLoginComponent = ({ onSuccess }) => {
  return (
    <GoogleLogin
      onSuccess={credentialResponse => {
        // Pass the token to the parent component
        onSuccess(credentialResponse.credential);
      }}
      onError={() => {
        console.error("Google login failed");
      }}
    />
  );
};

export default GoogleLoginComponent;
