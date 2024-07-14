export default interface Defect {
    id: number
    confidence: number
    type: { name: String, id: number, color: String}
    coordinates: { x: number, y: number, w: number, h: number }
}