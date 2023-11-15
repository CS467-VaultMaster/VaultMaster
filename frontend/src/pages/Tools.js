import React from "react";
import ExportPasswords from "../components/ExportPasswords";
import GeneratePassword from "../components/GeneratePassword";

export default function Tools() {
  return (
    <div className="tools">
      <h2>Tools</h2>
      <ExportPasswords />
      <GeneratePassword />
    </div>
  );
}
