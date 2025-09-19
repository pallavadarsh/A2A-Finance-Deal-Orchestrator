import React, { useEffect } from "react";
import { List, ListItem, ListItemText, Chip, Typography, Stack } from "@mui/material";

const typeColors: Record<string, "primary"|"secondary"|"success"|"error"|"warning"|"info"> = {
  PROPOSE: "info",
  REQUEST: "primary",
  INFORM: "secondary",
  ADVISE: "warning",
  ACCEPT: "success",
  REJECT: "error",
  HUMAN_APPROVE: "success",
  HUMAN_REVISE: "warning",
};

export default function Timeline({ runId, timeline, setTimeline }: any) {
  useEffect(() => {
    if (!runId) return;
    const fetchTimeline = async () => {
      const res = await fetch(`http://localhost:8010/trace/${runId}/timeline`);
      const data = await res.json();
      setTimeline(data.timeline || []);
    };
    fetchTimeline();
    const interval = setInterval(fetchTimeline, 4000);
    return () => clearInterval(interval);
  }, [runId]);

  return (
    <>
      <Typography variant="h6" gutterBottom>Trace Timeline</Typography>
      <List>
        {timeline.map((line: string, i: number) => {
          const type = line.match(/—(\w+)→/)?.[1];
          return (
            <ListItem key={i} divider>
              <Stack direction="row" spacing={2} alignItems="center">
                {type && <Chip label={type} color={typeColors[type] || "default"} size="small" />}
                <ListItemText primary={line} />
              </Stack>
            </ListItem>
          );
        })}
      </List>
    </>
  );
}
