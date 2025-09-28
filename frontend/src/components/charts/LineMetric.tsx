import React from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

type Props = { data: Array<{ ts: string; value: number }> }

export default function LineMetric({ data }: Props) {
  return (
    <ResponsiveContainer width="100%" height={250}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="ts" hide />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="value" dot={false} isAnimationActive={false} />
      </LineChart>
    </ResponsiveContainer>
  )
}
