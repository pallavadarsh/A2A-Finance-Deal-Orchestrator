import React, { useState } from "react";
import { TextField, Button, Typography, Stack } from "@mui/material";

export default function DealForm({ setRunId, setDraft, setTimeline }: any) {
  const [dealJson, setDealJson] = useState<string>(`{
  "deal_name":"Project Falcon",
  "target":{"name":"Acme FinTech","sector":"FinTech","region":"APAC"},
  "financials":{"revenue":120.0,"ebitda":24.0,"debt":30.0},
  "purchase_price":220.0,
  "currency":"USD"
}`);

  const startDeal = async () => {
    try {
      const res = await fetch("http://localhost:8010/deal/start", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: dealJson,
      });
      const data = await res.json();
      setRunId(data.run_id);
      setDraft(data.draft);
      setTimeline([]);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <>
      <Typography variant="h6" gutterBottom>Start a Deal</Typography>
      <Stack spacing={2}>
        <TextField multiline minRows={6} value={dealJson} onChange={(e)=>setDealJson(e.target.value)} />
        <Button variant="contained" onClick={startDeal}>Submit Deal</Button>
      </Stack>
    </>
  );
}
