import axios from "axios";

export function passwordComplexity(password) {
  if (password.length < 8) {
    return false;
  }
  return true;
}

// Uses browser native crypto feature since crypto-js is dead
export async function sha1Hash(data) {
  const encoder = new TextEncoder();
  const encodedData = encoder.encode(data);
  const digest = await crypto.subtle.digest("SHA-1", encodedData);
  return Array.from(new Uint8Array(digest))
    .map((byte) => byte.toString(16).padStart(2, "0"))
    .join("")
    .toUpperCase();
}

export async function hasPasswordBeenPwned(password) {
  let hashedPwd;
  try {
    hashedPwd = await sha1Hash(password);
  } catch (error) {
    console.error("Error hashing password: ", error);
    return false; // If hashing fails, we assume password hasn't been Pwnd
  }

  // Only send the prefix to the API
  const prefix = hashedPwd.slice(0, 5);
  const suffix = hashedPwd.slice(5);

  try {
    const response = await axios.get(`https://api.pwnedpasswords.com/range/${prefix}`);
    const data = response.data;
    return data.split("\n").some((line) => line.startsWith(suffix)); // True if so
  } catch (error) {
    console.error("Error checking HIBP database: ", error);
    return false; // Error means it hasn't been Pwnd
  }
}

// Use this around the program rather than repeating it so much
export function verifyToken() {
  const token = sessionStorage.getItem("authToken");
  if (!token) {
    console.error("No authentication token found.");
    return null;
  }
  return token;
}
