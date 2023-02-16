import type { AppProps } from "next/app";
import { ChainId, ThirdwebProvider } from "@thirdweb-dev/react";
import "../styles/globals.css";
import React, { useEffect, useState } from "react";

// This is the chainId your dApp will work on.
const activeChainId = ChainId.Sepolia;

function MyApp({ Component, pageProps }: AppProps) {

  const [data, setData] = useState([{}])

  useEffect(() => {
    fetch("/winner").then(
      res => res.json()
    ).then(
      data => {
        setData(data)
        console.log(data);
      }
    )
  }, [])

  
  return (
    <ThirdwebProvider desiredChainId={activeChainId}>
      <Component {...pageProps} />
    </ThirdwebProvider>
  );
}

export default MyApp;
