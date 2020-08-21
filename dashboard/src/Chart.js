import React from 'react';
import { useTheme } from '@material-ui/core/styles';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Label,
  ResponsiveContainer,
} from 'recharts';
import Title from './Title';

// Generate Sales Data
function createData(time, amount) {
  return { time, amount };
}
/*
const data = [
  createData('00:00', 0),
  createData('03:00', 300),
  createData('06:00', 600),
  createData('09:00', 800),
  createData('12:00', 1500),
  createData('15:00', 2000),
  createData('18:00', 2400),
  createData('21:00', 2400),
  createData('24:00', undefined),
];
*/
export default function Chart(props) {
  const theme = useTheme();
  return (
    <React.Fragment>
      <Title> Historical Vehicle Count</Title>
      <ResponsiveContainer>
        <LineChart
          data={props.data}
          margin={{
            top: 16,
            right: 16,
            bottom: 0,
            left: 24,
          }}
        >
          <XAxis dataKey="time" stroke={theme.palette.text.secondary} />
          <YAxis stroke={theme.palette.text.secondary}>
            <Label
              angle={270}
              position="left"
              style={{
                textAnchor: 'middle',
                fill: theme.palette.text.primary,
              }}
            >
              Count
            </Label>
          </YAxis>
          <Line
            type="monotone"
            dataKey="car"
            stroke={theme.palette.primary.main}
            dot={false}
          />
          <Line
            type="monotone"
            dataKey="truck"
            stroke={theme.palette.primary.secondary}
            dot={false}
          />
          <Line
            type="monotone"
            dataKey="garbage truck"
            stroke={theme.palette.primary.error}
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </React.Fragment>
  );
}
