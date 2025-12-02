########################################
# TensorFlow Lite
########################################
-keep class org.tensorflow.lite.** { *; }
-keep interface org.tensorflow.lite.* { *; }

########################################
# ONNX Runtime
########################################
-keep class ai.onnxruntime.** { *; }

########################################
# Keep model classes
########################################
-keep class com.arm.adaptiveintelligence.** { *; }
