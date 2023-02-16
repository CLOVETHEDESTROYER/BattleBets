import type { NextApiRequest, NextApiResponse } from 'next';
import axios from 'axios';


export default async function handler(
  res: NextApiResponse
) {
  const result = await axios.get('http://localhost:8000/winner');
  res.status(200).json(result.data);
}
// export default async function handler(req, res) {
//     const response = await fetch('http://localhost:8000/winner');

