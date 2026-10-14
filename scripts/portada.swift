// Portada de un vídeo: el fotograma de un segundo dado, en JPEG.
// Sin ffmpeg: usa AVFoundation, que ya trae macOS.
//
//   swiftc -O -o /tmp/portada scripts/portada.swift
//   /tmp/portada videos/clima-es.mp4 portadas/clima-es.jpg 3 1280
import AVFoundation
import AppKit

let args = CommandLine.arguments
guard args.count >= 3 else {
    print("uso: portada <video.mp4> <salida.jpg> [segundo=3] [ancho=1280]")
    exit(1)
}
let segundo = args.count > 3 ? Double(args[3])! : 3
let ancho = args.count > 4 ? Double(args[4])! : 1280

let generador = AVAssetImageGenerator(asset: AVURLAsset(url: URL(fileURLWithPath: args[1])))
generador.appliesPreferredTrackTransform = true
generador.maximumSize = CGSize(width: ancho, height: ancho)
generador.requestedTimeToleranceBefore = .zero
generador.requestedTimeToleranceAfter = .zero

let imagen = try generador.copyCGImage(at: CMTime(seconds: segundo, preferredTimescale: 600), actualTime: nil)
let jpeg = NSBitmapImageRep(cgImage: imagen).representation(using: .jpeg, properties: [.compressionFactor: 0.8])!
try jpeg.write(to: URL(fileURLWithPath: args[2]))
print(args[2], imagen.width, "x", imagen.height, jpeg.count / 1024, "KB")
