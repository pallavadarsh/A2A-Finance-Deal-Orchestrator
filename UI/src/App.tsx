import React, { useState } from "react";
import { Container, Grid, Paper, Typography } from "@mui/material";
import DealForm from "./components/DealForm";
import DraftMemo from "./components/DraftMemo";
import FinalMemo from "./components/FinalMemo";
import Timeline from "./components/Timeline";

export default function App() {
  const [runId, setRunId] = useState<string | null>(null);
  const [draft, setDraft] = useState<string>("");
  const [finalMemo, setFinalMemo] = useState<string>("");
  const [timeline, setTimeline] = useState<string[]>([]);

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>
        🚀 A2A Investment Banking + TechOps Demo
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <DealForm setRunId={setRunId} setDraft={setDraft} setTimeline={setTimeline} />
            <DraftMemo draft={draft} />
            <FinalMemo runId={runId} setFinalMemo={setFinalMemo} finalMemo={finalMemo} />
          </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Timeline runId={runId} timeline={timeline} setTimeline={setTimeline} />
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
}
