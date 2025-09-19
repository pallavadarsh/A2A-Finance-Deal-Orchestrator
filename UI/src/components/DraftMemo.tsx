import React from "react";
import { Typography, Paper } from "@mui/material";

export default function DraftMemo({ draft }: any) {
  if (!draft) return null;
  return (
    <Paper sx={{ mt: 2, p: 2, bgcolor: "#f5f5f5" }}>
      <Typography variant="h6">Draft Memo</Typography>
      <Typography>{draft}</Typography>
    </Paper>
  );
}
