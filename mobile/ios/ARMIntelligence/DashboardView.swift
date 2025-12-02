import SwiftUI

struct DashboardView: View {
    @StateObject private var viewModel = DashboardViewModel()
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                Text("ARM Adaptive Intelligence")
                    .font(.title)
                    .fontWeight(.bold)
                    .padding(.bottom)
                
                Text(viewModel.statusMessage)
                    .padding()
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .background(Color.gray.opacity(0.2))
                    .cornerRadius(8)
                
                VStack(alignment: .leading, spacing: 10) {
                    Text("Performance Metrics")
                        .font(.headline)
                    
                    VStack(alignment: .leading, spacing: 8) {
                        MetricRow(label: "CPU", value: String(format: "%.1f%%", viewModel.metrics.cpuUsage))
                        MetricRow(label: "Memory", value: "\(viewModel.metrics.memoryUsedMB)/\(viewModel.metrics.memoryMaxMB) MB")
                        MetricRow(label: "Battery", value: "\(viewModel.metrics.batteryPercent)%")
                        MetricRow(label: "Temperature", value: String(format: "%.1f°C", viewModel.metrics.temperature))
                    }
                    .padding()
                    .background(Color.white)
                    .cornerRadius(8)
                }
                
                VStack(alignment: .leading, spacing: 10) {
                    Text("Actions")
                        .font(.headline)
                    
                    Button(action: viewModel.compressModel) {
                        Text("Compress Model")
                            .frame(maxWidth: .infinity)
                            .padding()
                            .background(viewModel.isInitialized ? Color.blue : Color.gray)
                            .foregroundColor(.white)
                            .cornerRadius(8)
                    }
                    .disabled(!viewModel.isInitialized)
                    
                    Button(action: viewModel.indexDocument) {
                        Text("Index Document")
                            .frame(maxWidth: .infinity)
                            .padding()
                            .background(viewModel.isInitialized ? Color.blue : Color.gray)
                            .foregroundColor(.white)
                            .cornerRadius(8)
                    }
                    .disabled(!viewModel.isInitialized)
                    
                    Button(action: viewModel.queryMemory) {
                        Text("Query Memory")
                            .frame(maxWidth: .infinity)
                            .padding()
                            .background(viewModel.isInitialized ? Color.blue : Color.gray)
                            .foregroundColor(.white)
                            .cornerRadius(8)
                    }
                    .disabled(!viewModel.isInitialized)
                }
            }
            .padding()
        }
        .onAppear {
            viewModel.initialize()
        }
    }
}

struct MetricRow: View {
    let label: String
    let value: String
    
    var body: some View {
        HStack {
            Text(label + ":")
                .fontWeight(.medium)
            Spacer()
            Text(value)
        }
    }
}

class DashboardViewModel: ObservableObject {
    @Published var statusMessage = "Initializing..."
    @Published var metrics = PerformanceMetrics()
    @Published var isInitialized = false
    
    private var timer: Timer?
    
    init() {}
    
    func initialize() {
        ARMEngine.shared.initialize { success, message in
            DispatchQueue.main.async {
                self.statusMessage = message
                self.isInitialized = success
                
                if success {
                    self.startMetricsUpdate()
                }
            }
        }
    }
    
    private func startMetricsUpdate() {
        timer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { _ in
            self.updateMetrics()
        }
    }
    
    private func updateMetrics() {
        if let metrics = ARMEngine.shared.getPerformanceMetrics() {
            DispatchQueue.main.async {
                self.metrics = metrics
            }
        }
    }
    
    func compressModel() {
        statusMessage = "Compressing model..."
        
        let documentsPath = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
        let modelPath = documentsPath.appendingPathComponent("models/sample_model.onnx").path
        let outputPath = documentsPath.appendingPathComponent("models/compressed_model.onnx").path
        
        ARMEngine.shared.compressModel(modelPath: modelPath, outputPath: outputPath, bits: 4) { success, message in
            DispatchQueue.main.async {
                self.statusMessage = message
            }
        }
    }
    
    func indexDocument() {
        statusMessage = "Indexing document..."
        
        let documentsPath = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
        let docPath = documentsPath.appendingPathComponent("documents/sample.txt").path
        
        ARMEngine.shared.indexDocument(documentPath: docPath) { success, message in
            DispatchQueue.main.async {
                self.statusMessage = message
            }
        }
    }
    
    func queryMemory() {
        statusMessage = "Querying memory..."
        
        ARMEngine.shared.queryMemory(query: "What is the main topic?") { success, message in
            DispatchQueue.main.async {
                self.statusMessage = success ? "Query Result:\n\(message)" : message
            }
        }
    }
    
    deinit {
        timer?.invalidate()
    }
}

struct DashboardView_Previews: PreviewProvider {
    static var previews: some View {
        DashboardView()
    }
}
