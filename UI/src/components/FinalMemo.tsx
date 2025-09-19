import React from "react";
import { Button, Typography, Paper, Stack } from "@mui/material";

export default function FinalMemo({ runId, setFinalMemo, finalMemo }: any) {
  const sendReview = async (decision: string) => {
    try {
      const res = await fetch("http://localhost:8010/deal/review", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ run_id: runId, decision, feedback: "Demo feedback" }),
      });
      const data = await res.json();
      setFinalMemo(data.final);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <>
      {runId && !finalMemo && (
        <Stack direction="row" spacing={2} sx={{ mt: 2 }}>
          <Button variant="contained" color="success" onClick={()=>sendReview("approve")}>
            Approve
          </Button>
          <Button variant="contained" color="warning" onClick={()=>sendReview("revise")}>
            Revise
          </Button>
        </Stack>
      )}
      {finalMemo && (
        <Paper sx={{ mt: 2, p: 2, bgcolor: "#e3f2fd" }}>
          <Typography variant="h6">Final Memo</Typography>
          <Typography>{finalMemo}</Typography>
        </Paper>
      )}
    </>
  );
}
