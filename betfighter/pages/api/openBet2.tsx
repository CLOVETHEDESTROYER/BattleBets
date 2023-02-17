import type { NextApiRequest, NextApiResponse } from 'next';
import axios from 'axios';


export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const result = await axios.get('/');
  console.log(req);
  res.status(200).json(result.data);
}
// export default async function handler(req, res) {
//     const response = await fetch('http://localhost:8000/winner');

