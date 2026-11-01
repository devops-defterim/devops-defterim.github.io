import Foundation
import Vision
import AppKit

let dir = CommandLine.arguments[1]
let outPath = CommandLine.arguments[2]
let files = try FileManager.default.contentsOfDirectory(atPath: dir).filter { $0.hasSuffix(".png") }.sorted()
var result: [String: Any] = [:]
for f in files {
    let url = URL(fileURLWithPath: dir).appendingPathComponent(f)
    guard let img = NSImage(contentsOf: url), let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else { continue }
    let req = VNRecognizeTextRequest()
    req.recognitionLevel = .accurate
    req.recognitionLanguages = ["tr-TR", "en-US"]
    req.usesLanguageCorrection = false
    let handler = VNImageRequestHandler(cgImage: cg, options: [:])
    try? handler.perform([req])
    var lines: [[String: Any]] = []
    for obs in req.results ?? [] {
        guard let cand = obs.topCandidates(1).first else { continue }
        let s = cand.string
        var words: [[String: Any]] = []
        var idx = s.startIndex
        for w in s.split(separator: " ", omittingEmptySubsequences: true) {
            guard let r = s.range(of: w, range: idx..<s.endIndex) else { continue }
            idx = r.upperBound
            if let bb = try? cand.boundingBox(for: r)?.boundingBox {
                words.append(["t": String(w), "b": [bb.minX, bb.minY, bb.width, bb.height]])
            }
        }
        let bb = obs.boundingBox
        lines.append(["t": s, "b": [bb.minX, bb.minY, bb.width, bb.height], "w": words])
    }
    result[String(f.dropLast(4))] = ["w": cg.width, "h": cg.height, "lines": lines]
}
let data = try JSONSerialization.data(withJSONObject: result, options: [])
try data.write(to: URL(fileURLWithPath: outPath))
print("OCR:", result.count)
