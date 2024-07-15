export default interface Defect {
    id: number
    confidence: number
    type: { name: string, id: number, color: string}
    coordinates: string
}
//{ x: number, y: number, w: number, h: number }