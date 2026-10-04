import React from "react";
import { createBrowserRouter } from "react-router-dom";

import App from "./App";

import HomePage from "../pages/Home/HomePage";
import ConversationPage from "../pages/Conversation/ConversationPage";
import DebugPage from "../pages/Debug/DebugPage";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      {
        index: true,
        element: <HomePage />,
      },
      {
        path: "conversation",
        element: <ConversationPage />,
      },
      {
        path: "debug",
        element: <DebugPage />,
      },
    ],
  },
]);
