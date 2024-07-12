export default interface Defect {
    id: number
    confidence: number
    type: { type: String, id: number}
    coordinates: { x: number, y: number, w: number, h: number }
}