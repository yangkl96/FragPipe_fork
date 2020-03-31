package com.github.chhh.utils;

import com.dmtavt.fragpipe.exceptions.UnexpectedException;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class ProcessUtils {
  private static final Logger log = LoggerFactory.getLogger(ProcessUtils.class);

  private ProcessUtils() {}

  /** Coalesces output lines with '\n' characters. */
  public static String captureOutput(ProcessBuilder pb) throws UnexpectedException {
    return String.join("\n", captureOutputLines(pb));
  }

  public static List<String> captureOutputLines(ProcessBuilder pb) throws UnexpectedException {
    pb.redirectErrorStream(true);
    List<String> lines = new ArrayList<>();
    log.debug("Starting process to capture output: {}", String.join(" ", pb.command()));
    int code;
    try {
      Process p = pb.start();
      try (BufferedReader br = new BufferedReader(new InputStreamReader(p.getInputStream()))) {
        String line;
        while ((line = br.readLine()) != null) {
          lines.add(line);
        }
      } catch (IOException e) {
        throw new UnexpectedException(e);
      }
      code = p.waitFor();
    } catch (InterruptedException | IOException e) {
      throw new UnexpectedException(e);
    }
    log.debug("Got return code {} from process: {}", code, String.join(" ", pb.command()));
    return lines;
  }
}
