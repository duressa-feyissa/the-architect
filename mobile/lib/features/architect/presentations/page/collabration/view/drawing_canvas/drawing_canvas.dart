import 'dart:async';
import 'dart:convert';

import 'package:architect/features/architect/presentations/page/collabration/view/drawing_canvas/models/drawing_mode.dart';
import 'package:architect/features/architect/presentations/page/collabration/view/drawing_canvas/models/sketch.dart';
import 'package:flutter/material.dart' hide Image;
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:socket_io_client/socket_io_client.dart' as IO;

class DrawingCanvas extends HookWidget {
  final double height;
  final double width;
  final ValueNotifier<Color> selectedColor;
  final ValueNotifier<double> strokeSize;
  final ValueNotifier<double> eraserSize;
  final ValueNotifier<DrawingMode> drawingMode;
  final ValueNotifier<Sketch?> currentSketch;
  final ValueNotifier<List<Sketch>> allSketches;
  final GlobalKey canvasGlobalKey;
  final ValueNotifier<int> polygonSides;
  final ValueNotifier<bool> filled;
  final String boardId;

  final Color kCanvasColor = const Color(0xfff2f3f7);

  DrawingCanvas({
    Key? key,
    required this.height,
    required this.width,
    required this.boardId,
    required this.selectedColor,
    required this.strokeSize,
    required this.eraserSize,
    required this.drawingMode,
    required this.currentSketch,
    required this.allSketches,
    required this.canvasGlobalKey,
    required this.filled,
    required this.polygonSides,
  }) : super(key: key);

  final IO.Socket socket = IO.io(
    'https://sketch-dq5zwrwm5q-ww.a.run.app',
    IO.OptionBuilder().setTransports(['websocket']).build(),
  )..connect();
  final currentSketchStream = StreamController<String>();
  final allSketchesStream = StreamController<String>();

  @override
  Widget build(BuildContext context) {
    socket.onConnect((_) {
      print('connect');
    });
    socket.on('currentSketch-$boardId', (data) {
      currentSketchStream.sink.add(data);
      currentSketch.value = Sketch.fromJson(jsonDecode(data));
    });

    socket.on('allSketches-$boardId', (data) {
      allSketchesStream.sink.add(data);
      allSketches.value = (jsonDecode(data) as List)
          .map((json) => Sketch.fromJson(json as Map<String, dynamic>))
          .toList();
    });

    useEffect(() {
      return () {
        currentSketchStream.close();
        currentSketchStream.sink.close();
        allSketchesStream.close();
        allSketchesStream.sink.close();
        socket.disconnect();
      };
    }, []);

    return Stack(
      children: [
        buildAllPaths(),
        buildCurrentPath(context),
      ],
    );
  }

  Widget buildAllPaths() {
    return StreamBuilder(
      stream: allSketchesStream.stream,
      builder: (context, snapshot) {
        List<Sketch> sketches = List.empty(growable: true);
        List sketchesMap = List.empty(growable: true);

        if (snapshot.hasData) {
          sketchesMap = jsonDecode(snapshot.data!);
          sketches = sketchesMap
              .map((json) => Sketch.fromJson(json as Map<String, dynamic>))
              .toList();
        }

        return RepaintBoundary(
          child: SizedBox(
            height: height,
            width: width,
            child: CustomPaint(
              painter: SketchPainter(sketches: sketches),
            ),
          ),
        );
      },
    );
  }

  Widget buildCurrentPath(BuildContext context) {
    return StreamBuilder(
        stream: currentSketchStream.stream,
        builder: (context, snapshot) {
          Sketch? sketch;
          Map<String, dynamic>? sketchMap;
          if (snapshot.hasData) {
            sketchMap = jsonDecode(snapshot.data!);
          }
          if (sketchMap != null) {
            sketch = Sketch.fromJson(sketchMap);
          }
          return Listener(
            onPointerDown: (details) {
              final box = context.findRenderObject() as RenderBox;
              final offset = box.globalToLocal(details.position);

              currentSketch.value = Sketch(
                points: [offset],
                color: drawingMode.value == DrawingMode.eraser
                    ? kCanvasColor
                    : selectedColor.value,
                size: drawingMode.value == DrawingMode.eraser
                    ? eraserSize.value
                    : strokeSize.value,
                type: () {
                  switch (drawingMode.value) {
                    case DrawingMode.line:
                      return SketchType.line;
                    case DrawingMode.circle:
                      return SketchType.circle;
                    case DrawingMode.square:
                      return SketchType.rectangle;
                    default:
                      return SketchType.scribble;
                  }
                }(),
              );
            },
            onPointerMove: (details) {
              final box = context.findRenderObject() as RenderBox;
              final offset = box.globalToLocal(details.position);

              final points =
                  List<Offset>.from(currentSketch.value?.points ?? [])
                    ..add(offset);
              currentSketch.value = Sketch(
                points: points,
                color: drawingMode.value == DrawingMode.eraser
                    ? kCanvasColor
                    : selectedColor.value,
                size: drawingMode.value == DrawingMode.eraser
                    ? eraserSize.value
                    : strokeSize.value,
                type: () {
                  switch (drawingMode.value) {
                    case DrawingMode.line:
                      return SketchType.line;
                    case DrawingMode.circle:
                      return SketchType.circle;
                    case DrawingMode.square:
                      return SketchType.rectangle;
                    default:
                      return SketchType.scribble;
                  }
                }(),
              );

              socket.emit(
                  'currentSketch',
                  jsonEncode({
                    "id": boardId.toString(),
                    "currSketch": jsonEncode(currentSketch.value)
                  }));
            },
            onPointerUp: (details) {
              allSketches.value = [
                ...allSketches.value,
                currentSketch.value!,
              ];

              socket.emit('allSketches', boardId.toString());
            },
            child: RepaintBoundary(
              child: SizedBox(
                height: height,
                width: width,
                child: CustomPaint(
                  painter: SketchPainter(
                    sketches: sketch == null ? [] : [sketch],
                  ),
                ),
              ),
            ),
          );
        });
  }
}

class SketchPainter extends CustomPainter {
  final List<Sketch> sketches;

  SketchPainter({required this.sketches});

  @override
  void paint(Canvas canvas, Size size) {
    for (Sketch sketch in sketches) {
      final points = sketch.points;

      final path = Path();
      path.moveTo(points.first.dx, points.first.dy);

      for (int i = 1; i < points.length - 1; ++i) {
        final p0 = points[i];
        final p1 = points[i + 1];
        path.quadraticBezierTo(
          p0.dx,
          p0.dy,
          (p0.dx + p1.dx) / 2,
          (p0.dy + p1.dy) / 2,
        );
      }

      Paint paint = Paint()
        ..color = sketch.color
        ..strokeWidth = sketch.size
        ..strokeCap = StrokeCap.round
        ..style = PaintingStyle.stroke;

      Offset firstPoint = sketch.points.first;
      Offset lastPoint = sketch.points.last;

      Rect rect = Rect.fromPoints(firstPoint, lastPoint);
      if (sketch.type == SketchType.scribble) {
        canvas.drawPath(path, paint);
      } else if (sketch.type == SketchType.line) {
        canvas.drawLine(firstPoint, lastPoint, paint);
      } else if (sketch.type == SketchType.circle) {
        canvas.drawOval(rect, paint);
      } else if (sketch.type == SketchType.rectangle) {
        canvas.drawRect(rect, paint);
      }
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) {
    return true;
  }
}
